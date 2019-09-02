from rest_framework import serializers
from main.models import User, Client, Employee, Category, Booking
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .backends import ModelBackend



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def partial_update(self, instance, validated_data):
        Client.objects.get(pk=instance.id).update(**validated_data)
        queryset = Client.objects.filter(pk=instance.id).update(**validated_data)
        return queryset


class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {'password':{'write_only': True}}
        
    def create(self, validated_data):
        print(validated_data)
        client = Client(
            email = validated_data['email'],
            fullname = validated_data['fullname'], 
            phone = validated_data['phone'],
            cardno = validated_data['cardno'],
            password = validated_data['password']
        )
        client.save()
        return client

class ClientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField()

    def validate(self, data):
        user = ModelBackend.authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError(str(user))

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'

    def partial_update(self, instance, validated_data):
        Category.objects.get(pk=instance.id).update(**validated_data)
        queryset = Category.objects.filter(pk=instance.id).update(**validated_data)
        return queryset
    
    def create(self, validated_data):
        category = Category(
            name = validated_data['name']
        )
        category.save()
        return category



# EMPLOYEE SERIALIZER
class EmployeeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    booking_count = serializers.IntegerField(source="book", read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'fullname',
            'empno',
            'email',
            'phone',
            'category', 
            'is_active',
            'password',
            'photo',
            'empno',
            'profile',
            'booking_count'
            ]

    def partial_update(self, instance, validated_data):
        Employee.objects.get(pk=instance.id).update(**validated_data)
        queryset = Employee.objects.filter(pk=instance.id).update(**validated_data)
        return queryset

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {'password':{'write_only': True}}
        
    def create(self, validated_data):
        ema = validated_data['email']
        employee = Employee(
            email = validated_data['email'],
            fullname = validated_data['fullname'], 
            phone = validated_data['phone'],
            photo = validated_data['photo'],
            profile = validated_data['profile'],
            category = validated_data['category'],
            empno = validated_data['empno'],
            password = validated_data['password']
        )
        employee.save()
        return employee

class EmployeeLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField()

    def validate(self, data):
        user = ModelBackend.authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError(str(user))

class BookingSerializer(serializers.ModelSerializer):
    bempno = EmployeeSerializer(read_only=True)
    bcardno = ClientSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def partial_update(self, instance, validated_data):
        Booking.objects.get(pk=instance.id).update(**validated_data)
        queryset = Booking.objects.filter(pk=instance.id).update(**validated_data)
        return queryset
    
    def create(self, validated_data):
        booking = Booking(
            bempno = validated_data['bempno'],
            bcardno = validated_data['bcardno'],
            date_booked = validated_data['date_booked'],
            time_booked = validated_data['time_booked'],
            duration = validated_data['duration'],
            comment = validated_data['comment'],
        )
        booking.save()
        return booking

class BookingRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    class Meta:
        model = User
 
    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)
 
        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = ModelBackend().authenticate(email=email, password=password)
        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            userObj = Employee.objects.get(email=user.email)
        except Employee.DoesNotExist:
            userObj = None 
 
        try:
            if userObj is None:
                userObj = Client.objects.get(email=user.email)
        except Client.DoesNotExist:
                raise serializers.ValidationError(
                'User with given email and password does not exists2'
            )      
 
        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return userObj