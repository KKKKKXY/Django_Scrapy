import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScrapyAppComponent } from './scrapy-app.component';

describe('ScrapyAppComponent', () => {
  let component: ScrapyAppComponent;
  let fixture: ComponentFixture<ScrapyAppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ScrapyAppComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ScrapyAppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
