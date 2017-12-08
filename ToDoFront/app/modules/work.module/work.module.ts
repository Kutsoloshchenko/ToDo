// Module that governs user sign in, sign up, password restoration

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from "@angular/http";
import { FormsModule} from '@angular/forms';

import { AlbumRouterModule } from "./modules/album-router.module"
import { UserFolderComponent } from "./components/user-folder.component/user-folder.component"
import { AlbumService } from './services/album.service';

@NgModule({
    declarations: [
      UserFolderComponent      
      ],
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        AlbumRouterModule
      ],
    providers: [AlbumService],
})
export class AlbumsModule{}
