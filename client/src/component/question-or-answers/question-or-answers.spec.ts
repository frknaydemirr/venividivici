import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuestionOrAnswers } from './question-or-answers';

describe('QuestionOrAnswers', () => {
  let component: QuestionOrAnswers;
  let fixture: ComponentFixture<QuestionOrAnswers>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QuestionOrAnswers]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuestionOrAnswers);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
