import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {Navigation} from './components/navigation/navigation';
import {ShortenForm} from './components/shorten-form/shorten-form';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Navigation, ShortenForm],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
