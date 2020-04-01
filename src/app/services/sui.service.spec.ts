import { TestBed } from '@angular/core/testing';

import { SuiService } from './sui.service';

describe('SuiService', () => {
  let service: SuiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SuiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
