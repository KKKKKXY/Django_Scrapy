import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendAPIService {

  baseurl = 'http://localhost:1200';
  httpHeaders = new HttpHeaders({'Content-Type': 'application/json'});

  constructor(private http: HttpClient) { }

  getAllFiles(): Observable<any>{
    return this.http.get(this.baseurl + '/all_files/', {headers: this.httpHeaders});
  }
}
