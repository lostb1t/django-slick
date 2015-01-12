

var slick = angular.module('slick', ['ngResource', 'ui.router', 'formly'])
    .run(function($http, $rootScope, $state, $stateParams) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
    });


slick.factory("AppResource", function($resource) {
  return $resource("/admin/api/app/:app_label/", { app_label: '@_app_label'});
});


slick.factory("ModelResource", function($resource) {
    return $resource("/admin/api/:app_label/:model/:pk/", { app_label: '@_app_label', model: '@_model', pk: '@_pk'}, { 
        schema: {
                method: 'GET',
                isArray: true,
                url: '/admin/api/:app_label/:model/schema/',
                /*
                transformResponse: function(data, header) {
                  //console.log(data['name']);

                  var wrapped = angular.fromJson(data);

                  //console.log(wrapped.actions.POST);
                  //console.log(wrapped.actions.POST.data);
                  //return d.promise;
                  return wrapped.actions.POST;
                  //return fields;
                }
                */
                
            }
        }
    );
});


slick.config(function ($stateProvider, $urlRouterProvider, $resourceProvider) {
    $urlRouterProvider.otherwise('/');

    // TODO base on django setting
    $resourceProvider.defaults.stripTrailingSlashes = false;

    var template_base_path = '/static/slick/templates/';

    $stateProvider
      .state('objects', {
        abstract: true,
        url: '/:app_label/:model',
        templateUrl: template_base_path + 'partials/objects.html',
      })
      .state('objects.list', {
        url: '',
        parent: 'objects',
        views: {
            '': {
                templateUrl: template_base_path + 'partials/list.html',
                controller: 'ListViewCtrl'
            }  
        }
      })
      .state('objects.list.detail', {
        parent: 'objects.list',
        url: '/:pk',
        views: {
            'detail@objects.list': {
                templateUrl: template_base_path + 'partials/update_form.html',
                controller: 'UpdateViewCtrl'
            }
        }
      });

 });


slick.controller('ListViewCtrl', function($scope, $state, $stateParams, AppResource, ModelResource) {
    AppResource.get({ app_label: $stateParams.app_label}, function(data) {
        $scope.app = data;
        
        angular.forEach(data['models'], function(model, key) {
            if (angular.equals(model.name, $stateParams.model)) {
                $scope.model = model;
            }
        });
    })

    ModelResource.query({ app_label: $stateParams.app_label, model: $stateParams.model}, function(data) {
        $scope.objects = data;
    })

    $scope.DetailView = function(app_label, model, id) {
        $state.go('objects.list.detail', {pk: id});
    }
});


slick.controller('UpdateViewCtrl', function($scope, $stateParams, $http, AppResource, ModelResource) {
    console.log("UpdateViewCtrl called");
    
    var response = ModelResource.schema({ app_label: $stateParams.app_label, model: $stateParams.model});
    response.$promise.then(function(data) {
        $scope.formData = {};
        $scope.formFields = data;
    });

    var response = ModelResource.get({ app_label: $stateParams.app_label, model: $stateParams.model, pk: $stateParams.pk});
    response.$promise.then(function(data) {
        $scope.formData = data;
    });

});

slick.controller("sidebar", function ($scope, $stateParams, AppResource) {
    console.log("sidebar called");

    AppResource.query(function(data) {
        //console.log(data);
        $scope.apps = data;
    })
});

