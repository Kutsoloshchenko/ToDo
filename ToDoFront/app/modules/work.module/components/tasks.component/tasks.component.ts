// Component that responseble for signing user up

import { Component, Input} from "@angular/core";
import { JWTAuthService } from "../../../../services/jwt-auth.service"
import { TaskService } from "../../services/tasks.service"
import { Router } from "@angular/router"
import { OnInit } from "@angular/core/src/metadata/lifecycle_hooks";
import { Task } from '../../classes/tasks';
import { Project } from '../../classes/projects'
import { forEach } from "@angular/router/src/utils/collection";

@Component({
    selector: "tasks",
    templateUrl: "./tasks.component.html",
    styleUrls: ["./tasks.component.scss"]
})
export class TasksComponent implements OnInit {

    /*Name of the logged in user */
    username: string;

    error_message: string;

    empty_message: string;

    tasks: Task[];

    projects: Project[];

    showCreate: boolean;
    
    /*Constructor in whitch jwtAuth service is injected */
    constructor(private jwtAuth: JWTAuthService, private taskService: TaskService){}

    ngOnInit(): void {
        
                /*Methor that is called during initialization of component*/
        
                this.username = this.jwtAuth.getUserName() // get user name first time
        
                this.jwtAuth.usernameChange.subscribe(
                (user) => this.username = user );          // subscribe to username chage to recive new one as soon as user log ins or logs out

                this.getTasksForToday();
                this.showCreate = false;
                console.log(this.tasks)

            }

    getTasksForToday(): void{

        this.taskService.GetTodayTasks(this.username, this.jwtAuth.getToken())
        .then(server_responce => 
         { if (server_responce[0].name != undefined)
            {
            this.tasks = server_responce;
            this.tasks.forEach(task => {
                                this.getPriorotiColor(task)
                                        })
            }
        else
            {
                this.empty_message = "No items for today!"
            }
          
        })
        }

    getTasksFor7Days(): void{
            
         this.taskService.Get7DaysTasks(this.username, this.jwtAuth.getToken())
        .then(server_responce => 
            { if (server_responce[0].name != undefined)
                {
                this.tasks = server_responce;
                this.tasks.forEach(task => {
                                    this.getPriorotiColor(task)
                                            })
                }
            else
                {
                    this.tasks = [];
                    this.empty_message = "No items for next 7 days!"
                }
              
            })
            }

    getDoneTasks(): void{
            
         this.taskService.GetDoneTasks(this.username, this.jwtAuth.getToken())
        .then(server_responce => 
            { if (server_responce[0].name != undefined)
                {
                this.tasks = server_responce;
                this.tasks.forEach(task => {
                                    this.getPriorotiColor(task)
                                            })
                }
            else
                {
                    this.tasks = [];
                    this.empty_message = "No done tasks! Get to work!"
                }
              
            })
            }

            
    getTasksForProject(project_id: number): void {
        this.taskService.GetProjectTasks(this.username, this.jwtAuth.getToken(), project_id)
        .then(server_responce => 
         { 
             if (server_responce[0].name != undefined)
            {
            this.tasks = server_responce;
            this.tasks.forEach(task => {
                                this.getPriorotiColor(task)
                                        })
            }
            else
            {
                this.tasks = [];
                this.empty_message = "No tasks in this project"
            }
          
        })
        }



    changeTask(task: Task, name: string, priority: number, state: string, due_date: Date): void{

        console.log(task.project_id)

        this.taskService.ChangeTask(this.username, this.jwtAuth.getToken(), name, priority, due_date, state, task.id, task.project_id)
                         .then(server_responce => {
                             if (server_responce.result == "Ok")
                             {
                                this.getTasksForToday()
                             }
                             else {
                                 this.error_message = server_responce.error;
                             }
                            })
                            }
    deleteTask(task: Task): void{

                this.taskService.DeleteTask(this.username, this.jwtAuth.getToken(), task.id)
                                 .then(server_responce => {
                                     if (server_responce.result == "Ok")
                                     {
                                        this.getTasksForToday()
                                     }
                                     else {
                                        this.error_message = server_responce.error;
                                     }
                                    })
            }

    createTask( name: string, priority: number, project: number, due_date: Date): void{
                
                this.taskService.CreateTask(this.username, this.jwtAuth.getToken(), name, priority, due_date, project)
                                  .then(server_responce => {
                                             if (server_responce.result == "Ok")
                                             {
                                                this.getTasksForToday()
                                                this.showCreate = false;
                                             }
                                             else {
                                                this.error_message = server_responce.error;
                                             }
                                            })
                    }
        
    getPriorotiColor(task: Task): void {
        switch(task.priority) {
            
                        case 1: {
                            task.priority_color = "red";
                            break;
                        }
            
                        case 2: {
                            task.priority_color = "orange";
                            break;
                        }
            
                        case 3: {
                            task.priority_color = "green";
                            break;
                        }
            
                    }
    }

    ShowCreate(): void{
        this.showCreate = true;
    }

    editTask(task: Task): void {
        if (task.change == true)
        { task.change=false }
        else
        { task.change = true }
    }

    getNewProjects(projects: Project[]): void{
        this.projects = projects
    }

    Print(name, priority, project, date): void {
        console.log(name, priority, project, date)
    }

}
