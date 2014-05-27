'use strict'

angular
  .module('taarifaWaterpointsApp', [
    'ngResource',
    'ngRoute',
    'leaflet-directive',
    'dynform',
    'angular-flash.service',
    'angular-flash.flash-alert-directive'
  ])
  .config ($routeProvider, flashProvider) ->
    $routeProvider
      .when '/',
        templateUrl: 'views/main.html'
        controller: 'MapCtrl'
      .when '/waterpoints/edit/:id',
        templateUrl: 'views/edit.html'
        controller: 'WaterpointEditCtrl'
      .when '/waterpoints/new',
        templateUrl: 'views/edit.html'
        controller: 'WaterpointCreateCtrl'
      .when '/requests/new',
        templateUrl: 'views/edit.html'
        controller: 'RequestCreateCtrl'
      .when '/dashboard',
        templateUrl: 'views/dashboard.html'
        controller: 'DashboardCtrl'
      .otherwise
        redirectTo: '/'
    flashProvider.errorClassnames.push 'alert-danger'
