import { Component } from '@angular/core';
import { BackendAPIService } from './backend-api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [BackendAPIService]
})
export class AppComponent {
  title = 'my-app';
  companies = [{company_id: ''}];

  constructor(private api: BackendAPIService){
    this.getThaiCompanies();
  }

  getThaiCompanies = () => {
    this.api.getAllThaiCompanies().subscribe(
      data => {
        console.log(data);
        this.companies = data;
      },
      error => {
        console.log(error);
      }
    );

  }
}
