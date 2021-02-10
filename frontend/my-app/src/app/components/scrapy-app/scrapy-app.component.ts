import { Component, OnInit } from '@angular/core';
// import { Component, OnInit, ViewChild } from '@angular/core';
// import { MatPaginator, MatTableDataSource } from '@angular/material';

// import {AfterViewInit, Component, ViewChild} from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {Observable} from 'rxjs';
import {map, startWith} from 'rxjs/operators';

import { BackendAPIService } from '../../backend-api.service';


/////
@Component({
  selector: 'app-scrapy-app',
  templateUrl: './scrapy-app.component.html',
  styleUrls: ['./scrapy-app.component.css'],
  providers: [BackendAPIService]
})

export class ScrapyAppComponent implements OnInit {
  myControl = new FormControl();
  option: string[] = ['One', 'Two', 'Three'];
  filteredOptions: Observable<string[]>;

  options: FormGroup;
  // filesControl = new FormControl('dbd_2020.xlsx');
  // browsersControl = new FormControl(5, Validators.min(10));
  // companies = [{company_id: ''}];

  filesControl = new FormControl('dbd_2020.xlsx', [Validators.required]);
  browsersControl = new FormControl(5, [Validators.required, Validators.min(1), Validators.max(5)]);

  constructor(fb: FormBuilder, private api: BackendAPIService) {
    this.options = fb.group({
      file: this.filesControl,
      browsers: this.browsersControl,
    });
    // this.runThaiSpider();
  }

  runThaiSpider = () => {
    console.log(this.browsersControl.value);
    console.log(this.filesControl.value);
    this.api.runThaiSpider().subscribe(
      data => {
        console.log(data);
        // this.companies = data;
      },
      error => {
        console.log(error);
      }
    );

  }

  ngOnInit() {
    this.filteredOptions = this.myControl.valueChanges
      .pipe(
        startWith(''),
        map(value => this._filter(value))
      );
  }

  // getFontSize() {
  //       return Math.max(10, this.fontSizeControl.value);
  //     }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.option.filter(option => option.toLowerCase().includes(filterValue));
  }

  // tslint:disable-next-line: typedef
  // submit(){
  //   console.log(this.browsersControl.value);
  //   console.log(this.filesControl.value);

  // }
}

// export class ScrapyAppComponent{
//   options: FormGroup;
//   colorControl = new FormControl('primary');
//   fontSizeControl = new FormControl(16, Validators.min(10));
//   constructor(fb: FormBuilder) {
//     this.options = fb.group({
//       color: this.colorControl,
//       fontSize: this.fontSizeControl,
//     });
//   }

//   getFontSize() {
//     return Math.max(10, this.fontSizeControl.value);
//   }
// }

// // export class ScrapyAppComponent implements OnInit {

// //   constructor() { }

// //   ngOnInit(): void {
// //   }
// // }
