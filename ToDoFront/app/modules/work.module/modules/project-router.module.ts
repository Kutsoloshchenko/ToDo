// router for AuthModule 

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from "@angular/router";
import { MasterComponent }  from "../components/master.component/master.component"


const routes: Routes = [
    {path: "projects", component:MasterComponent},
]

@NgModule ({
    imports: [ RouterModule.forChild(routes)],
    exports: [ RouterModule ]
})
export class ProjectRouterModule {}