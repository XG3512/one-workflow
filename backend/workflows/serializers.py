# -*- coding: utf-8 -*-
# author: itimor

from workflows.models import *
from rest_framework import serializers


class WorkflowReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'
        depth = 1


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'

    def create(self, validated_data):
        roles = validated_data['roles']
        del validated_data['roles']
        obj = Workflow.objects.create(**validated_data)
        obj.roles.set(roles)
        obj.save()

        # 建立初始和结束状态
        State.objects.create(name="开始", order_id=1, state_type=1, is_hidden=True, participant_type=0, workflow=obj)
        State.objects.create(name="关闭", order_id=99, state_type=2, is_hidden=True, participant_type=0, workflow=obj)

        # 建立内置字段
        CustomField.objects.create(field_name="申请人", order_id=1, field_attribute=True, field_type=1,
                                   field_key="create_user", workflow=obj)
        CustomField.objects.create(field_name="申请时间", order_id=2, field_attribute=True, field_type=6,
                                   field_key="create_time", workflow=obj)
        CustomField.objects.create(field_name="部门", order_id=3, field_attribute=True, field_type=1, field_key="group",
                                   workflow=obj)
        CustomField.objects.create(field_name="工号", order_id=4, field_attribute=True, field_type=1, field_key="id",
                                   workflow=obj)

        return obj


class WorkflowTypeSerializer(serializers.ModelSerializer):
    workflow_list = serializers.SerializerMethodField()
    # workflow_set = WorkflowSerializer(many=True, read_only=True,)

    def get_workflow_list(self, instance):
        a = instance.workflow_set.get_queryset().filter(status=True)
        return a.values()

    class Meta:
        model = WorkflowType
        fields = '__all__'


class StateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
        depth = 1


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class TransitionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = '__all__'
        depth = 2


class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = '__all__'


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = '__all__'


class WorkflowBpmnSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowBpmn
        fields = '__all__'
