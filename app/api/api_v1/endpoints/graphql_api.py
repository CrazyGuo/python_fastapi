#Graph接口测试
'''
import graphene

class Person(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    full_name = graphene.String()
    sex = graphene.String()


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    def resolve_hello(self, info, name):
        return "Hello " + name
    #相当于user(age,sex)形式的接口
    users = graphene.String(age=graphene.Int(default_value=18), sex=graphene.String(default_value="femail"))
    def resolve_users(self, info, age, sex):
        result = []
        for x in range(5):
            result.append({'id': x,'age': age, 'sex': sex})
        return result
    #测试动态获取字段
    me = graphene.Field(Person)
    def resolve_me(parent, info):
        # returns an object that represents a Person
        p = Person
        p.first_name = 'Huanhuan'
        p.last_name = 'Guo'
        p.full_name = 'Huanhuan Guo JK'
        p.sex = 'M'
        return p  
'''