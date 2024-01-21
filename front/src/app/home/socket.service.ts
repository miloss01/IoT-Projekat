import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SocketService {

  constructor(private socket: Socket) { }

  getMessage() {
    return this.socket.fromEvent('probaSaServera').pipe(map((data: any) => data))
  }
}
