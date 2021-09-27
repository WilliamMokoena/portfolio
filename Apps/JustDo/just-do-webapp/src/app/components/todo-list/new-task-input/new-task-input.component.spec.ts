import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewTaskInputComponent } from './new-task-input.component';

describe('NewTaskInputComponent', () => {
  let component: NewTaskInputComponent;
  let fixture: ComponentFixture<NewTaskInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewTaskInputComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NewTaskInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
