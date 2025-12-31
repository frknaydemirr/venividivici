import { Layouts } from '../component/layouts/layouts';
import { Routes } from '@angular/router';
import { Home } from '../component/home/home';
import { Cities } from '../component/cities/cities';
import { Countries } from '../component/countries/countries';
import { QuestionOrAnswers } from '../component/question-or-answers/question-or-answers';
import { Login } from '../component/login/login';
import { inject } from '@angular/core';
import { AuthService } from '../app/services/auth'; // Dosya ismine göre güncelleyin
import { SignUp } from '../component/sign-up/sign-up';

export const routes: Routes = [
    { path: "login", component: Login },
    { path: "sign-up", component: SignUp },
    {
        path: "",
        component: Layouts,
        children: [
            { path: "", redirectTo: "home", pathMatch: "full" },
            { path: "home", component: Home },
            { path: "cities", component: Cities },
            { path: "countries", component: Countries },
            { path: "question-or-answers", component: QuestionOrAnswers } // canActivate kaldırıldı
        ]
    }
];