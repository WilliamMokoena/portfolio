import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TasksGroupComponent } from './tasks-group.component';

describe('TasksGroupComponent', () => {
  let component: TasksGroupComponent;
  let fixture: ComponentFixture<TasksGroupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TasksGroupComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TasksGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
