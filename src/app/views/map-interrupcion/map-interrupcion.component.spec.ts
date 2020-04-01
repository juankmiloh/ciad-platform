import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MapInterrupcionComponent } from './map-interrupcion.component';

describe('MapInterrupcionComponent', () => {
  let component: MapInterrupcionComponent;
  let fixture: ComponentFixture<MapInterrupcionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MapInterrupcionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MapInterrupcionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
