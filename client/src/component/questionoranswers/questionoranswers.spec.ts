import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Questionoranswers } from './questionoranswers';

describe('Questionoranswers', () => {
  let component: Questionoranswers;
  let fixture: ComponentFixture<Questionoranswers>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Questionoranswers]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Questionoranswers);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
