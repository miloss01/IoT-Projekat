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

  get_persons() {
    return this.socket.fromEvent('persons').pipe(map((data: any) => data))
  }

  get_DL() {
    return this.socket.fromEvent('DL').pipe(map((data: any) => data))
  }
  get_DPIR1() {
    return this.socket.fromEvent('DPIR1').pipe(map((data: any) => data))
  }
  get_DUS1() {
    return this.socket.fromEvent('DUS1').pipe(map((data: any) => data))
  }
}
