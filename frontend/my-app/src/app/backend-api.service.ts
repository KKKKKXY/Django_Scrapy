import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/internal/operators/catchError';

@Injectable({
  providedIn: 'root'
})
export class BackendAPIService {

  baseurl = 'http://localhost:1200';
  httpHeaders = new HttpHeaders({'Content-Type': 'application/json'});
  name = 'Thai';

  constructor(private http: HttpClient) { }

  getAllThaiCompanies(): Observable<any>{
    return this.http.get(this.baseurl + '/companies_thai/', {headers: this.httpHeaders});
  }

  runThaiSpider(){
    console.log('connect runThaiSpider service...');
    return this.http.post(this.baseurl + '/run_thai_spider/', {headers: this.httpHeaders});
  }
}
