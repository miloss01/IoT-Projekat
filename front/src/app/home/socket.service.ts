import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SocketService {

  flask_url: string = "http://localhost:5000"

  constructor(private socket: Socket, private http: HttpClient) { }

  getMessage() {
    return this.socket.fromEvent('probaSaServera').pipe(map((data: any) => data))
  }

  get_persons() {
    return this.socket.fromEvent('persons').pipe(map((data: any) => data))
  }
  get_alarm() {
    return this.socket.fromEvent('alarm').pipe(map((data: any) => data))
  }
  get_active() {
    return this.socket.fromEvent('active').pipe(map((data: any) => data))
  }
  send_pin(pin: string) {
    return this.http.post(this.flask_url + "/alarm_pin", {"pin": pin})
  }
  send_activate_pin(pin: string) {
    return this.http.post(this.flask_url + "/activate_pin", {"pin": pin})
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
  get_DS1() {
    return this.socket.fromEvent('DS1').pipe(map((data: any) => data))
  }
  get_DS2() {
    return this.socket.fromEvent('DS2').pipe(map((data: any) => data))
  }
  get_DB() {
    return this.socket.fromEvent('DB').pipe(map((data: any) => data))
  }
  get_RPIR1() {
    return this.socket.fromEvent('RPIR1').pipe(map((data: any) => data))
  }
  get_RPIR2() {
    return this.socket.fromEvent('RPIR2').pipe(map((data: any) => data))
  }
  get_RPIR3() {
    return this.socket.fromEvent('RPIR3').pipe(map((data: any) => data))
  }
  get_RPIR4() {
    return this.socket.fromEvent('RPIR4').pipe(map((data: any) => data))
  }
  get_GDHT_temp() {
    return this.socket.fromEvent('GDHT-temp').pipe(map((data: any) => data))
  }
  get_GDHT_hum() {
    return this.socket.fromEvent('GDHT-hum').pipe(map((data: any) => data))
  }
  get_B4SD() {
    return this.socket.fromEvent('B4SD').pipe(map((data: any) => data))
  }
}
