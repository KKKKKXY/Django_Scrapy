import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {FormBuilder, FormControl, FormGroup, FormArray, Validators} from '@angular/forms';
import { BackendAPIService } from '../../backend-api.service';

@Component({
  selector: 'app-file-manage-app',
  templateUrl: './file-manage-app.component.html',
  styleUrls: ['./file-manage-app.component.css'],
})
export class FileManageAppComponent implements OnInit {
  file: File;
  typeControl = new FormControl('', [Validators.required]);
  // options: FormGroup;
  selected: string;

  constructor(private http: HttpClient, private fb: FormBuilder, private api: BackendAPIService) {  }

  ngOnInit() { }

  onFileChanged(event: any){
    this.file = event.target.files[0];
    console.log(this.file);
  }

  newFile(){
    const uploadFile = new FormData();
    try{
      const uploadFileType = (this.file.name).substr((this.file.name).indexOf('.') + 1);
      uploadFile.append('filename', this.file.name);
      uploadFile.append('file', this.file, this.file.name);
      uploadFile.append('file_type', uploadFileType);

      if (uploadFileType !== this.typeControl.value){
        const errorMessage = `Message: Please select correct file type`;
        window.alert(errorMessage);
      }
      else{
        this.http.post('http://localhost:1200/upload_file/', uploadFile).subscribe(
          data => {
            console.log(data);
          },
          error => {
            console.log(error);
          }
        );
      }
    }
    catch (error){
      const errorMessage = `Message: Please upload file.`;
      window.alert(errorMessage);
    }
  }

}
