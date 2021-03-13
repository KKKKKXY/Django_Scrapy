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

  getAllThaiCompanies(): Observable<any>{
    return this.http.get(this.baseurl + '/companies_thai/', {headers: this.httpHeaders});
  }

  getThaiCaptchaEmail(): Observable<any>{
    console.log('Request capctha email...');
    return this.http.post(this.baseurl + '/send_thai_captcha_email/', {headers: this.httpHeaders});
  }

  getEngCaptchaEmail(): Observable<any>{
    console.log('Request capctha email...');
    return this.http.post(this.baseurl + '/send_eng_captcha_email/', {headers: this.httpHeaders});
  }

  // runThaiSpider(scraptItem: FormData): Observable<any>{
  //   console.log('connect runThaiSpider service...');
  //   return this.http.post(this.baseurl + '/run_thai_spider/', scraptItem, {headers: this.httpHeaders});
  // }

  // runEngSpider(captchaCode: string): Observable<any>{
  //   console.log('connect runEngSpider service...');
  //   return this.http.post(this.baseurl + '/run_eng_spider/', captchaCode, {headers: this.httpHeaders});
  // }

  // uploadFile(uploadData: FormData): Observable<any> {
  //   console.log(uploadData);
  //   return this.http.post(this.baseurl + '/upload_file/', uploadData, {headers: this.httpHeaders});
  // }

  getAllFiles(): Observable<any>{
    return this.http.get(this.baseurl + '/all_files/', {headers: this.httpHeaders});
  }
}
