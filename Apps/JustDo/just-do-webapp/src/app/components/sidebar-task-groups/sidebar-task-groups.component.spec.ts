import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SidebarTaskGroupsComponent } from './sidebar-task-groups.component';

describe('SidebarTaskGroupsComponent', () => {
  let component: SidebarTaskGroupsComponent;
  let fixture: ComponentFixture<SidebarTaskGroupsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SidebarTaskGroupsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SidebarTaskGroupsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
