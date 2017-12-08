// Component that responseble for signing user up

import { Component} from "@angular/core";
import { JWTAuthService } from "../../../../services/jwt-auth.service"
import { ProjectService } from "../../services//projects.service"
import { Router } from "@angular/router"
import { OnInit } from "@angular/core/src/metadata/lifecycle_hooks";
import { Project } from '../../classes/projects';

@Component({
    selector: "user-folder",
    templateUrl: "./user-folder.component.html",
    styleUrls: ["./user-folder.component.css"]
})
export class UserFolderComponent implements OnInit {
    /*Name of the logged in user */
    username: string;

    projects: Project[];

    create_album_name: string;
    
    /*Constructor in whitch jwtAuth service is injected */
    constructor(private jwtAuth: JWTAuthService, private projectService: ProjectService){}

    ngOnInit(): void {
        
                /*Methor that is called during initialization of component*/
        
                this.username = this.jwtAuth.getUserName() // get user name first time
        
                this.jwtAuth.usernameChange.subscribe(
                (user) => this.username = user );          // subscribe to username chage to recive new one as soon as user log ins or logs out

            }

    getProjects(): void{

        this.projectService.GetUserProjects(this.username, this.jwtAuth.getToken())
        .then(server_responce => 
         { console.log(server_responce)
            this.projects = server_responce;
         })
        }

    changeProjectName(folder_name: string, new_name: string): void{

        this.projectService.ChangeUserProject(this.username, this.jwtAuth.getToken(), folder_name, new_name)
                         .then(server_responce => {
                             if (server_responce.result == "Ok")
                             {
                                this.getProjects()
                             }
                             else {
                                 console.log(server_responce.error_message)
                             }
                            })
    }

    deleteProject(folder_name: string): void{
        
        console.log(folder_name)

                this.projectService.DeleteProject(this.username, this.jwtAuth.getToken(), folder_name)
                                 .then(server_responce => {
                                     if (server_responce.result == "Ok")
                                     {
                                        this.getProjects()
                                     }
                                     else {
                                         console.log(server_responce.error_message)
                                     }
                                    })
            }

    CreateProject( name: string, color: string): void{
                
                this.projectService.CreateProject(this.username, this.jwtAuth.getToken(), name, color)
                                  .then(server_responce => {
                                             if (server_responce.result == "Ok")
                                             {
                                                this.getProjects()
                                             }
                                             else {
                                                 console.log(server_responce.error_message)
                                             }
                                            })
                    }
        

}
