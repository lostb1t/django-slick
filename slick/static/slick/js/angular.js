

var slick = angular.module('slick', ['ngResource', 'ui.router'])
    .run(function($http, $rootScope) {

    });


slick.factory("AppResource", function($resource) {
  return $resource("/admin/api/app/:app_label/", { app_label: '@_app_label'});
});


slick.factory("ModelResource", function($resource) {
  return $resource("/admin/api/model/:app_label/:model/:pk/", { app_label: '@_app_label', model: '@_model', pk: '@_pk' });
});


slick.config(function ($stateProvider, $urlRouterProvider, $resourceProvider) {
    $urlRouterProvider.otherwise('/');

    // TODO base on django setting
    $resourceProvider.defaults.stripTrailingSlashes = false;

    var template_base_path = '/static/slick/templates/';

    $stateProvider
        .state('ListView', {
            url: '/:app_label/:model',
            controller: 'ListViewCtrl',
            templateUrl: template_base_path + 'partials/list.html'
        })
        .state('UpdateView', {
            url: '/:app_label/:model/:pk',
            controller: 'UpdateViewCtrl',
            templateUrl: template_base_path + 'partials/update_form.html'
        });
 });


slick.controller('ListViewCtrl', function($scope, $stateParams, AppResource, ModelResource) {

    AppResource.get({ app_label: $stateParams.app_label}, function(data) {
        $scope.app = data;
        console.log(data['models']);
        
        angular.forEach(data['models'], function(model, key) {
            if (angular.equals(model.name, $stateParams.model)) {
                console.log(model);
                $scope.model = model;
            }
        });
    })
    ModelResource.query({ app_label: $stateParams.app_label, model: $stateParams.model}, function(data) {
        $scope.objects = data;
    })
});


slick.controller('UpdateViewCtrl', function($scope, $stateParams, $http, AppResource, ModelResource) {
    // console.log($stateParams);

    $http.get('/admin/' + $stateParams.app_label + '/' + $stateParams.model  + '/ ' + $stateParams.pk  + '/')
        .success(function(data) {
            html = $(data);
            //console.log($('form'));
            //$scope.form_html = data;
        });

    /*
    r = $resource("/admin/:app_label/:model/:pk/", {app_label: '@_app_label', model: '@_model', pk: '@_pk' });
    r.get({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk}, function(data) {
        console.log(data);
        //$scope.objects = data;
    })
    */

    /*
    AppResource.query({ app_label: $stateParams.app_label}, function(data) {
        $scope.app = data;
        //$scope.model = data['models'][$stateParams.model];
    })
    ModelResource.query({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk}, function(data) {
        $scope.object = data;
    })
    */
});

slick.controller("sidebar", function ($scope, $stateParams, AppResource) {
    console.log("sidebar called");

    AppResource.query(function(data) {
        $scope.apps = data;
    })
});

