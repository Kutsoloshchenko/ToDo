// Module that governs user sign in, sign up, password restoration

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from "@angular/http";
import { FormsModule} from '@angular/forms';

import { ProjectRouterModule } from "./modules/project-router.module"
import { UserProjectComponent } from "./components/user-projects.component/user-project.component"
import { MasterComponent } from "./components/master.component/master.component"
import { TasksComponent } from "./components/tasks.component/tasks.component"
import { ProjectService } from './services/projects.service';
import { TaskService } from './services/tasks.service';

@NgModule({
    declarations: [
      UserProjectComponent,
      TasksComponent,
      MasterComponent      
      ],
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        ProjectRouterModule
      ],
    providers: [
      ProjectService,
      TaskService],
})
export class WorkModule{}
