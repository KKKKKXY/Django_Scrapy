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
  constructor(){ }

}
