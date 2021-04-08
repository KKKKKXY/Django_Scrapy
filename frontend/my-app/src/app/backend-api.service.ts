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


  getThaiCaptchaEmail(): Observable<any>{
    console.log('Request capctha email...');
    return this.http.post(this.baseurl + '/send_thai_captcha_email/', {headers: this.httpHeaders});
  }

  getEngCaptchaEmail(): Observable<any>{
    console.log('Request capctha email...');
    return this.http.post(this.baseurl + '/send_eng_captcha_email/', {headers: this.httpHeaders});
  }

  getAllFiles(): Observable<any>{
    return this.http.get(this.baseurl + '/all_files/', {headers: this.httpHeaders});
  }
}
