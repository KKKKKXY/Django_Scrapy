import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import { BackendAPIService } from '../../backend-api.service';

@Component({
  selector: 'app-scrapy-app',
  templateUrl: './scrapy-app.component.html',
  styleUrls: ['./scrapy-app.component.css'],
  providers: [BackendAPIService]
})

export class ScrapyAppComponent implements OnInit {
  scrapyOptions: FormGroup;
  thaiBrowserControl      = new FormControl('', [Validators.required]);
  engBrowserControl       = new FormControl('', [Validators.required]);
  selectThai              = new FormControl('', [Validators.required]);
  selectEng               = new FormControl('', [Validators.required]);
  reciEmailThaiControl    = new FormControl('', [Validators.required, Validators.email,]);
  reciEmailEngControl     = new FormControl('', [Validators.required, Validators.email,]);

  collection: Array<File> = [];
  captchaCode: any;

  constructor(fb: FormBuilder, private http: HttpClient, private api: BackendAPIService) {
    this.scrapyOptions = fb.group({
      thaiBrowser: this.thaiBrowserControl,
      engBrowser: this.engBrowserControl,
      selectthai: this.selectThai,
      selecteng: this.selectEng,
      reciThaiEmail: this.reciEmailThaiControl,
      reciEngEmail: this.reciEmailEngControl,
    });
  }

  ngOnInit() {
    this.getCollection();
  }

  getCollection() {
    this.api.getAllFiles().subscribe(
      data => {
        console.log(data);
        for (let i = 0; i < data.length; i++){
          this.collection.push(data[i].filename);
        }
      },
      error => {
        console.log(error);
      }
    );
  }

  runThaiSpider = () => {
    console.log(this.thaiBrowserControl.value);
    console.log(this.selectThai.toString());
    console.log(this.reciEmailThaiControl.value);

    const scraptItem = new FormData();
    scraptItem.append('reciemail', this.reciEmailThaiControl.value);

    // get captcha email
      this.http.post('http://localhost:1200/send_thai_captcha_email/', scraptItem).subscribe(
      data => {
        console.log(data);
      },
      error => {
        console.log(error);
      }
    );

    // if captcha code is valid, start to scrapy
    this.captchaCode = prompt('Please enter the capchacode that you got in inbox', '');
    console.log(this.captchaCode);
    if (this.captchaCode === '' || this.captchaCode === null){
      console.log('Cancel scrapy');
    }
    else{
      scraptItem.append('captchaCode', this.captchaCode);
      scraptItem.append('thaiBrowser', this.thaiBrowserControl.value);
      scraptItem.append('selectThai', this.selectThai.toString());

      this.http.post('http://localhost:1200/run_thai_spider/', scraptItem).subscribe(
        data => {
          console.log(data);
        },
        error => {
          console.log(error);
        }
      );

    }
  }

  runEngSpider = () => {
    console.log(this.engBrowserControl.value);
    console.log(this.selectEng.toString());
    console.log(this.reciEmailEngControl.value);

    const scraptItem = new FormData();
    scraptItem.append('reciemail', this.reciEmailEngControl.value);

    // get captcha email
    this.http.post('http://localhost:1200/send_eng_captcha_email/', scraptItem).subscribe(
      data => {
        console.log(data);
      },
      error => {
        console.log(error);
      }
    );

    // if captcha code is valid, start to scrapy
    this.captchaCode = prompt('Please enter the capchacode that you got in inbox', '');
    console.log(this.captchaCode);
    if (this.captchaCode === '' || this.captchaCode === null){
      console.log('Cancel scrapy');
    }
    else{
      scraptItem.append('captchaCode', this.captchaCode);
      scraptItem.append('engBrowser', this.engBrowserControl.value);
      scraptItem.append('selectEng', this.selectEng.toString());
      
      this.http.post('http://localhost:1200/run_eng_spider/', scraptItem).subscribe(
        data => {
          console.log(data);
        },
        error => {
          console.log(error);
        }
      );
    }
  }
}
