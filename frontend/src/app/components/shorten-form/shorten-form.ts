import {Component, inject, signal} from '@angular/core';
import {FormGroup, FormControl, Validators, ReactiveFormsModule} from '@angular/forms';
import {ShortenerService} from '../../services/shortener-service';
import {RouterLink, RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-shorten-form',
  imports: [ReactiveFormsModule, RouterOutlet, RouterLink, RouterOutlet],
  templateUrl: './shorten-form.html',
  styleUrl: './shorten-form.css',
})
export class ShortenForm {
  urlForm = new FormGroup({
    originalUrl: new FormControl("", [Validators.required, Validators.pattern('https?://.+')])
  })

  showError = signal(false);
  isShaking = signal(false);
  shortenedUrl = signal<string | null>(null);
  shortenerService = inject(ShortenerService);
  showServerError = signal(false);

  triggerShake() {
    this.isShaking.set(true);
    this.showError.set(true);
    setTimeout(() => {
      this.isShaking.set(false);
    }, 800);
  }

  onSubmit() {
    if(this.urlForm.invalid) {
      this.triggerShake();
      this.urlForm.markAsTouched();
      return;
    } else {
      this.showError.set(false);
    }
    const rawUrl = this.urlForm.value.originalUrl;

    console.log("shortening url: ", rawUrl);

    this.shortenerService.shortenUrl(<string> rawUrl).subscribe({
      next: (response) => {
        console.log("Shortened URL received: ", response);
        this.shortenedUrl.set(response.short_url);
      },
      error: (err) => this.showServerError.set(true)
    })

  }


}
