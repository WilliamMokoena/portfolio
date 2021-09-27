import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopLogoBarComponent } from './top-logo-bar.component';

describe('TopLogoBarComponent', () => {
  let component: TopLogoBarComponent;
  let fixture: ComponentFixture<TopLogoBarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TopLogoBarComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TopLogoBarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
