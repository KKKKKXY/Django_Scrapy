import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FileManageAppComponent } from './components/file-manage-app/file-manage-app.component';
import { ScrapyAppComponent } from './components/scrapy-app/scrapy-app.component';

const routes: Routes = [
  { path: 'scrapy', pathMatch: 'full', component: ScrapyAppComponent},
  { path: 'file-management', pathMatch: 'full', component: FileManageAppComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
