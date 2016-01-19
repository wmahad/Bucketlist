'use strict';


var app = angular.module('BucketListApp', ['ui.router', 'angularMoment', 'ngResource','ngStorage']);
 
app.config(function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
 
    $stateProvider
    
    //States for auth
    .state('signup', {
        url: '/signup',
        controller: 'AuthController',
        templateUrl: '/static/views/signup.html'
    })

    .state('login', {
        url: '/login',
        controller: 'AuthController',
        templateUrl: '/static/views/login.html'
    })

    .state('logout', {
        url: '/logout',
        controller: function ($rootScope, $state, $localStorage, BucketListService) {
            BucketListService.UserAuth.logout(function () {
                $localStorage.reset();
                $state.go('signup');
            });
            $state.go('signup');
        },
        module: 'private'
    })

    //States for bucketlist  
    .state('viewBucket', {
        url: '/bucketlist/:id/items',
        controller: 'BucketListViewController',
        templateUrl: '/static/views/bucketlist_view.html',
        module: 'private'
    })


    .state('dashboard', {
        url: '/bucketlists',
        controller: 'BucketListController',
        templateUrl: '/static/views/dashboard.html',
        module: 'private'
    });
       

    $urlRouterProvider.otherwise('/signup');

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('httpRequestInterceptor');

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
});
 
app.run(function($rootScope, $state, $localStorage) {

    $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
        if (toState.module === 'private' && !$localStorage.authenticated) {
            // If logged out and transitioning to a logged in page:
            event.preventDefault();
            $state.go('login',{}, {reload:true});
        }

    });
});






