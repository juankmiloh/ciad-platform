import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProcesosDiegComponent } from './procesos-dieg.component';

describe('ProcesosDiegComponent', () => {
  let component: ProcesosDiegComponent;
  let fixture: ComponentFixture<ProcesosDiegComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProcesosDiegComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProcesosDiegComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
