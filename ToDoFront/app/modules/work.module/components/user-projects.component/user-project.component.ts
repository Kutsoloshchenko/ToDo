// Component that responseble for signing user up

import { Component, Input} from "@angular/core";
import { JWTAuthService } from "../../../../services/jwt-auth.service"
import { ProjectService } from "../../services//projects.service"
import { Router } from "@angular/router"
import { OnInit } from "@angular/core/src/metadata/lifecycle_hooks";
import { Project } from '../../classes/projects';
import { TasksComponent } from "../tasks.component/tasks.component"

@Component({
    selector: "user-project",
    templateUrl: "./user-project.component.html",
    styleUrls: ["./user-project.component.scss"]
})
export class UserProjectComponent implements OnInit {
    @Input()
    tasksref: TasksComponent;
    
    /*Name of the logged in user */
    username: string;

    error_message: string;
    
    empty_message: string;

    projects: Project[];

    showCreate: boolean;

    create_album_name: string;
    
    /*Constructor in whitch jwtAuth service is injected */
    constructor(private jwtAuth: JWTAuthService, private projectService: ProjectService){}

    ngOnInit(): void {
        
                /*Methor that is called during initialization of component*/
        
                this.username = this.jwtAuth.getUserName() // get user name first time
        
                this.jwtAuth.usernameChange.subscribe(
                (user) => this.username = user );          // subscribe to username chage to recive new one as soon as user log ins or logs out

                this.getProjects();
                this.showCreate = false;

            }

    getProjects(): void{

        this.projectService.GetUserProjects(this.username, this.jwtAuth.getToken())
        .then(server_responce => 
         { if (server_responce[0].name != undefined)
            {
            this.projects = server_responce;
            this.tasksref.getNewProjects(this.projects)
            }
            else
            {
                this.projects = [];
                this.empty_message = "No projects"
            }
         })
        }

    changeProjectName(project: Project, name: string, color: string): void{

        this.projectService.ChangeUserProject(this.username, this.jwtAuth.getToken(), name, color ,project.id )
                         .then(server_responce => {
                             if (server_responce.result == "Ok")
                             {
                                this.getProjects()
                             }
                             else {
                                this.error_message = server_responce.error
                             }
                            })
    }
    deleteProject(project: Project): void{

                this.projectService.DeleteProject(this.username, this.jwtAuth.getToken(), project.id)
                                 .then(server_responce => {
                                     if (server_responce.result == "Ok")
                                     {
                                        this.getProjects()
                                     }
                                     else {
                                         this.error_message = server_responce.error
                                     }
                                    })
            }

    CreateProject( name: string, color: string): void{
                
                this.projectService.CreateProject(this.username, this.jwtAuth.getToken(), name, color)
                                  .then(server_responce => {
                                             if (server_responce.result == "Ok")
                                             {
                                                this.getProjects()
                                                this.showCreate = false;
                                             }
                                             else {
                                                this.error_message = server_responce.error
                                             }
                                            })
                    }
        
    getProjectTasks(project: Project): void {
        this.tasksref.getTasksForProject(project.id)
    }

    ShowCreate(): void{
        this.showCreate = true;
    }

    editProject(project: Project): void {
        if (project.changes == true)
        { project.changes=false }
        else
        { project.changes = true }
    }

}
