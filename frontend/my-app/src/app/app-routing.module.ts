import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ScrapyAppComponent } from './components/scrapy-app/scrapy-app.component';

const routes: Routes = [
  { path: 'scrapy', pathMatch: 'full', component: ScrapyAppComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
