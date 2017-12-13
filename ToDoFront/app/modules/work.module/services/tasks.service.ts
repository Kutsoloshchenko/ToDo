// Service that makes http request to server reguarding authorization 

import { Injectable } from '@angular/core';
import { Http, Headers } from "@angular/http";
import { Task } from '../classes/tasks'

import 'rxjs/add/operator/toPromise';



@Injectable()
export class TaskService{

    // Rest API link
    private restAPILink = "http://127.0.0.1:8000"

    // constructor that injects HTTP client
    constructor(private http : Http){}

    public GetProjectTasks(username: string, token: string, project: number): Promise<Task[]> {
        const body = ({username: username,
                       token: token,
                       project: project
                    })
        
        return this.http
                   .post(this.restAPILink+"/get_tasks_for_project/", body)
                   .toPromise()
                   .then(result => result.json() as Task[])

    }

    public GetTodayTasks(username: string, token: string): Promise<Task[]> {
        const body = ({username: username,
                       token: token
                    })
        
        return this.http
                   .post(this.restAPILink+"/get_tasks_for_today/", body)
                   .toPromise()
                   .then(result => result.json() as Task[])

    }

    public Get7DaysTasks(username: string, token: string): Promise<Task[]> {
        const body = ({username: username,
                       token: token
                    })
        
        return this.http
                   .post(this.restAPILink+"/get_tasks_for_7_days/", body)
                   .toPromise()
                   .then(result => result.json() as Task[])

    }

    public GetDoneTasks(username: string, token: string): Promise<Task[]> {
        const body = ({username: username,
                       token: token
                    })
        
        return this.http
                   .post(this.restAPILink+"/get_done_tasks/", body)
                   .toPromise()
                   .then(result => result.json() as Task[])

    }

    public DeleteTask(username: string, token: string, id: number): Promise<Task> {
        const body = ({username: username,
                       token: token,
                       id: id})
        
        return this.http
                   .post(this.restAPILink+"/delete_task/", body)
                   .toPromise()
                   .then(result => result.json() as Task)

    }

    public ChangeTask(username: string, token: string, name: string, priority: number, due_date: Date, state: string, id: number, project: number): Promise<Task> {
        const body = ({username: username,
                       token: token,
                       name: name,
                       priority: priority,
                       due_date: due_date,
                       state: state,
                       project: project,
                       id: id})

        return this.http
                   .post(this.restAPILink+"/change_task/", body)
                   .toPromise()
                   .then(result => result.json() as Task)

    }

    public CreateTask(username: string, token: string, name: string, priority: number, due_date: Date, project: number): Promise<Task> {
        const body = ({username: username,
                       token: token,
                       name: name,
                       priority: priority,
                       due_date: due_date,
                       project: project
                    })
        
        return this.http
                   .post(this.restAPILink+"/create_task/", body)
                   .toPromise()
                   .then(result => result.json() as Task)

    }


}