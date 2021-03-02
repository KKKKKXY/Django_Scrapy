import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileManageAppComponent } from './file-manage-app.component';

describe('FileManageAppComponent', () => {
  let component: FileManageAppComponent;
  let fixture: ComponentFixture<FileManageAppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FileManageAppComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FileManageAppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
