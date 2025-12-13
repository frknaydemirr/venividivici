import { Layouts } from '../component/layouts/layouts';
import { Routes } from '@angular/router';
import { Home } from '../component/home/home';
import { Cities } from '../component/cities/cities';
import { Countries } from '../component/countries/countries';
import { QuestionOrAnswers } from '../component/question-or-answers/question-or-answers';
import { Login } from '../component/login/login';
import { inject } from '@angular/core';
import { Auth } from './services/auth';


export const routes: Routes = [
    {
            path:"login",
            component:Login
    },

    {
        path:"",
        component:Layouts,
        canActivateChild : [() => (inject(Auth) as Auth)],
        children: [
            {
            path:"",
            component:Home

            },{

               path:"cities",
               component: Cities 
            },
            {
                path:"countries",
                component: Countries
            },
            {
                path:"questionsoranswers",
                component: QuestionOrAnswers
            },

             

        ]
        
    }

];