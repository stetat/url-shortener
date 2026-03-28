import { Routes } from '@angular/router';
import {AboutUs} from './components/about-us-component/about-us';
import {ShortenForm} from './components/shorten-form/shorten-form';
import {Contacts} from './components/contacts/contacts';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: ShortenForm },
  { path: 'about', component: AboutUs },
  { path: 'contacts', component: Contacts },
];
