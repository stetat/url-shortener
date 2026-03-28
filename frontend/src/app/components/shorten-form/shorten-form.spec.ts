import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShortenForm } from './shorten-form';

describe('ShortenForm', () => {
  let component: ShortenForm;
  let fixture: ComponentFixture<ShortenForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShortenForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShortenForm);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
