// Service that makes http request to server reguarding authorization 

import { Injectable } from '@angular/core';
import { Http, Headers } from "@angular/http";
import { Project } from '../classes/projects';
import { Task } from '../classes/tasks'

import 'rxjs/add/operator/toPromise';



@Injectable()
export class ProjectService{

    // Rest API link
    private restAPILink = "http://127.0.0.1:8000"

    // constructor that injects HTTP client
    constructor(private http : Http){}

    public GetUserProjects(username: string, token: string): Promise<Project[]> {
        const body = ({username: username,
                       token: token})
        
        return this.http
                   .post(this.restAPILink+"/get_projects/", body)
                   .toPromise()
                   .then(result => result.json() as Project[])

    }

    public DeleteProject(username: string, token: string, id: number): Promise<Project> {
        const body = ({username: username,
                       token: token,
                       id: id})
        
        return this.http
                   .post(this.restAPILink+"/delete_project/", body)
                   .toPromise()
                   .then(result => result.json() as Project)

    }

    public ChangeUserProject(username: string, token: string, name: string, color: string, id: number): Promise<Project> {
        const body = ({username: username,
                       token: token,
                       name: name,
                       color: color,
                       id: id})
        
        return this.http
                   .post(this.restAPILink+"/change_project/", body)
                   .toPromise()
                   .then(result => result.json() as Project)

    }

    public CreateProject(username: string, token: string, name: string, color: string): Promise<Project> {
        const body = ({username: username,
                       token: token,
                       name: name,
                       color: color
                    })
        
        return this.http
                   .post(this.restAPILink+"/create_project/", body)
                   .toPromise()
                   .then(result => result.json() as Project)

    }


}