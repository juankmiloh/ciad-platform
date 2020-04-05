import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MapPqrsComponent } from './map-pqrs.component';

describe('MapPqrsComponent', () => {
  let component: MapPqrsComponent;
  let fixture: ComponentFixture<MapPqrsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MapPqrsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MapPqrsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
