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
  get_clock() {
    return this.socket.fromEvent('clock').pipe(map((data: any) => data))
  }
  send_clock(time: string) {
    return this.http.post(this.flask_url + "/clock_time", {"time": time})
  }
  stop_clock() {
    return this.http.post(this.flask_url + "/stop_clock", {})
  }
  send_rgb(rgb: string) {
    return this.http.post(this.flask_url + "/rgb", { "rgb": rgb })
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
  get_DPIR2() {
    return this.socket.fromEvent('DPIR2').pipe(map((data: any) => data))
  }
  get_DUS2() {
    return this.socket.fromEvent('DUS2').pipe(map((data: any) => data))
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
  get_BB() {
    return this.socket.fromEvent('BB').pipe(map((data: any) => data))
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
  get_GSG() {
    return this.socket.fromEvent('GSG').pipe(map((data: any) => data))
  }
  get_BIR() {
    return this.socket.fromEvent('BIR').pipe(map((data: any) => data))
  }
  
  get_RDHT1_temp() {
    return this.socket.fromEvent('RDHT1-temp').pipe(map((data: any) => data))
  }
  get_RDHT1_hum() {
    return this.socket.fromEvent('RDHT1-hum').pipe(map((data: any) => data))
  }
  get_RDHT2_temp() {
    return this.socket.fromEvent('RDHT2-temp').pipe(map((data: any) => data))
  }
  get_RDHT2_hum() {
    return this.socket.fromEvent('RDHT2-hum').pipe(map((data: any) => data))
  }
  get_RDHT3_temp() {
    return this.socket.fromEvent('RDHT3-temp').pipe(map((data: any) => data))
  }
  get_RDHT3_hum() {
    return this.socket.fromEvent('RDHT3-hum').pipe(map((data: any) => data))
  }
  get_RDHT4_temp() {
    return this.socket.fromEvent('RDHT4-temp').pipe(map((data: any) => data))
  }
  get_RDHT4_hum() {
    return this.socket.fromEvent('RDHT4-hum').pipe(map((data: any) => data))
  }
}
