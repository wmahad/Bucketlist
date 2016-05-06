'use strict';

app.factory('BucketListService', function ($resource) {

    return {
        auth: $resource('/api/api-token-auth/', {}, {
            login: {
                method: 'POST'
            }           
        },{
            stripTrailingSlashes: false
        }),
        verify: $resource('/api/api-token-verify/', {}, {
            token: {
                method: 'POST'
            }
        }, {
            stripTrailingSlashes: false
        }),

        users: $resource('/api/auth/signup/', {}, {
            create: {
                method: 'POST'
            }
        },{
            stripTrailingSlashes: false
        }),

        Bucketlists: $resource("/api/bucketlists/:id/", {id: "@id"}, {
            createBucket: {
                method: 'POST'
            }, 
            getAllBuckets: {
                method: 'GET',
                isArray: true
            },
            getOneBucket: {
                method: 'GET',
                isArray: false
            },
            updateBucket:  { 
                method: 'PUT' 
            },
            deleteBucket: {
                method: 'DELETE'
            }
        },{
            stripTrailingSlashes: false
        }),

        BucketlistItems: $resource("/api/bucketlists/:bid/items/:id/", {bid:"@bid", id: "@id"}, {
            createBucketItem: {
                method: 'POST'
            },
            getOneBucketItem: {
                method: 'GET',
                isArray: false
            },
            updateBucketItem:  { 
                method: 'PUT' 
            },
            deleteBucketItem: {
                method: 'DELETE'
            }
        },{
            stripTrailingSlashes: false
        })
    };
});


app.factory('httpRequestInterceptor', function ($localStorage) {
    return {
        request: function(config) {
            var token = $localStorage.token;
            config.headers = config.headers || {};
            if (token) {
                config.headers['Authorization'] = 'JWT ' + token;
            }
            
            return config;
        }
    };
});
