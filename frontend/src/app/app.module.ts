import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HttpClientModule} from '@angular/common/http';
import { ProductsComponent } from './products/products.component';
import { LoginComponent } from './login/login.component';
import {FormsModule} from '@angular/forms';
import { CaddyComponent } from './caddy/caddy.component';
import { ProductComponent } from './product/product.component';


@NgModule({
  declarations: [
    AppComponent,
    ProductsComponent,
    LoginComponent,
    CaddyComponent,
    ProductComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule, HttpClientModule,FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})


export class AppModule { }
