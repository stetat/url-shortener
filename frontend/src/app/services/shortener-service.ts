import { Injectable, inject, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {ShortenUrlResponse} from '../models/shorten-url-response';
import {Observable} from 'rxjs';
import {environment} from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ShortenerService {
  http = inject(HttpClient);
  private readonly API_URL = `${environment.apiUrl}/links/shorten/`;

  shortenUrl(originalUrl: string): Observable<ShortenUrlResponse> {
    return this.http.post<ShortenUrlResponse>(this.API_URL, {
      original_url: originalUrl
    });
  }
}
