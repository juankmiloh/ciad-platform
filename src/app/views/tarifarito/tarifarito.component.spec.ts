import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TarifaritoComponent } from './tarifarito.component';

describe('TarifaritoComponent', () => {
  let component: TarifaritoComponent;
  let fixture: ComponentFixture<TarifaritoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TarifaritoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TarifaritoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
