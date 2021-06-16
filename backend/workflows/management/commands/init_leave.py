# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password

from workflows.models import *
from systems.models import *


class Command(BaseCommand):
    help = '假期工作流'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('############ 配置工作流用户角色 ###########'))
        topgroup = Group.objects.get(name='top', code='top')

        group_ops = Group.objects.create(name='运维', code='ops', sequence=1, parent=topgroup)
        group_dev = Group.objects.create(name='开发', code='dev', sequence=2, parent=topgroup)
        group_hr = Group.objects.create(name='人事', code='hr', sequence=3, parent=topgroup)

        self.stdout.write(self.style.SUCCESS('############ 初始化角色 ###########'))
        toprole = Role.objects.get(name='top', code='top')

        role_ops_tl = Role.objects.create(name='运维经理', code='ops_tl', sequence=1, group=group_ops, parent=toprole)
        role_ops = Role.objects.create(name='运维', code='ops', sequence=1, group=group_ops, parent=toprole)
        role_dev_tl = Role.objects.create(name='开发经理', code='dev_tl', sequence=2, group=group_dev, parent=toprole)
        role_dev = Role.objects.create(name='开发', code='dev', sequence=2, group=group_dev, parent=toprole)
        role_hr_tl = Role.objects.create(name='人事经理', code='hr_tl', sequence=3, group=group_hr, parent=toprole)
        role_hr = Role.objects.create(name='人事', code='hr', sequence=3, group=group_hr, parent=toprole)

        self.stdout.write(self.style.SUCCESS('############ 初始化用户 ###########'))
        ops_tl = User.objects.create(username='ops_tl', password=make_password("123456"), realname="青龙",
                                     group=group_ops)
        ops_tl.roles.add(role_ops_tl)
        ops = User.objects.create(username='ops', password=make_password("123456"), realname="白虎", group=group_ops)
        ops.roles.add(role_ops)
        dev_tl = User.objects.create(username='dev_tl', password=make_password("123456"), realname="朱雀",
                                     group=group_dev)
        dev_tl.roles.add(role_dev_tl)
        dev = User.objects.create(username='dev', password=make_password("123456"), realname="玄武", group=group_dev)
        dev.roles.add(role_dev)
        hr_tl = User.objects.create(username='hr_tl', password=make_password("123456"), realname="霸下", group=group_hr)
        hr_tl.roles.add(role_hr_tl)
        hr = User.objects.create(username='hr', password=make_password("123456"), realname="青鸾", group=group_hr)
        hr.roles.add(role_hr)

        self.stdout.write(self.style.SUCCESS('############ 请假工作流 ###########'))
        ## 工作流类型
        ad_type = WorkflowType.objects.create(name='行政', code='ad', order_id=1)

        ## 工作流
        leave_wf = Workflow.objects.create(name='请假单', type=ad_type, ticket_sn_prefix='leave')

        ## 工作流字段
        # 建立内置字段
        CustomField.objects.create(field_name="申请人", order_id=1, field_attribute=True, field_type=1,
                                   field_key="create_user", workflow=leave_wf)
        CustomField.objects.create(field_name="申请时间", order_id=2, field_attribute=True, field_type=6,
                                   field_key="create_time", workflow=leave_wf)
        CustomField.objects.create(field_name="部门", order_id=3, field_attribute=True, field_type=1, field_key="group",
                                   workflow=leave_wf)
        CustomField.objects.create(field_name="工号", order_id=4, field_attribute=True, field_type=2, field_key="id",
                                   workflow=leave_wf)
        # 建立扩展字段
        c1 = CustomField.objects.create(field_name="请假时间", order_id=10, field_type=7, field_key="start_end_time",
                                        workflow=leave_wf)
        c2 = CustomField.objects.create(field_name="请假类型", order_id=30, field_type=9, field_key="type",
                                        field_choice='{"1":"病假", "2":"产假"}', workflow=leave_wf)
        c3 = CustomField.objects.create(field_name="事由说明", order_id=50, field_type=8, field_key="memo",
                                        workflow=leave_wf)
        c4 = CustomField.objects.create(field_name="领导审批", order_id=60, field_type=9, field_key="leader_radio",
                                        field_choice='{"1":"同意", "2":"不同意"}', workflow=leave_wf)
        c5 = CustomField.objects.create(field_name="人事审批", order_id=80, field_type=9, field_key="hr_radio",
                                        field_choice='{"1":"同意", "2":"不同意"}', workflow=leave_wf)

        # 建立初始和结束状态
        s1 = State.objects.create(name="开始", order_id=1, state_type=1, is_hidden=True, participant_type='none',
                                  workflow=leave_wf)
        s2 = State.objects.create(name="关闭", order_id=99, state_type=2, is_hidden=True, participant_type='none',
                                  workflow=leave_wf)
        # 建立流转状态
        s3 = State.objects.create(name="申请人-编辑中", order_id=2, participant_type='none', workflow=leave_wf)
        s3.fields.add(c1, c2, c3)
        s4 = State.objects.create(name="领导-审批中", order_id=3, participant_type='role', workflow=leave_wf)
        s4.fields.add(c4)
        s4.role_participant.add(role_ops_tl, role_dev_tl, role_hr_tl)
        s5 = State.objects.create(name="人事-审批中", order_id=4, participant_type='group', workflow=leave_wf)
        s5.fields.add(c5)
        s5.group_participant.add(group_hr)
        s6 = State.objects.create(name="结束", order_id=98, state_type=2, participant_type='none', workflow=leave_wf)

        # 建立工作流步骤
        Transition.objects.create(name=0, source_state=s1, dest_state=s3, attribute_type=0, workflow=leave_wf)
        Transition.objects.create(name=1, source_state=s1, dest_state=s4, attribute_type=1, workflow=leave_wf)

        Transition.objects.create(name=0, source_state=s3, dest_state=s3, attribute_type=0, workflow=leave_wf)
        Transition.objects.create(name=1, source_state=s3, dest_state=s4, attribute_type=1, workflow=leave_wf)
        Transition.objects.create(name=3, source_state=s3, dest_state=s6, attribute_type=3, workflow=leave_wf)

        Transition.objects.create(name=2, source_state=s4, dest_state=s3, attribute_type=2, workflow=leave_wf)
        Transition.objects.create(name=1, source_state=s4, dest_state=s5, attribute_type=1, workflow=leave_wf)

        Transition.objects.create(name=2, source_state=s5, dest_state=s3, attribute_type=2, workflow=leave_wf)
        Transition.objects.create(name=4, source_state=s5, dest_state=s2, attribute_type=5, workflow=leave_wf)

        self.stdout.write(self.style.SUCCESS('请假工作流完成'))

        self.stdout.write(self.style.SUCCESS('############ 发布工作流 ###########'))
        ## 工作流类型
        it_type = WorkflowType.objects.create(name='技术', code='it', order_id=2)

        ## 工作流
        deploy_wf = Workflow.objects.create(name='发布单', type=it_type, ticket_sn_prefix='deploy')

        ## 工作流字段
        # 建立内置字段
        CustomField.objects.create(field_name="申请人", order_id=1, field_attribute=True, field_type=1,
                                   field_key="create_user", workflow=deploy_wf)
        CustomField.objects.create(field_name="申请时间", order_id=2, field_attribute=True, field_type=6,
                                   field_key="create_time", workflow=deploy_wf)
        CustomField.objects.create(field_name="部门", order_id=3, field_attribute=True, field_type=1, field_key="group",
                                   workflow=deploy_wf)
        CustomField.objects.create(field_name="工号", order_id=4, field_attribute=True, field_type=2, field_key="id",
                                   workflow=deploy_wf)
        # 建立扩展字段
        c1 = CustomField.objects.create(field_name="发布时间", order_id=10, field_type=6, field_key="start_time",
                                        workflow=deploy_wf)
        c2 = CustomField.objects.create(field_name="发布项目", order_id=30, field_type=9, field_key="type",
                                        field_choice='{"1":"前端", "2":"后端"}', workflow=deploy_wf)
        c3 = CustomField.objects.create(field_name="发布内容", order_id=50, field_type=8, field_key="memo",
                                        workflow=deploy_wf)
        c4 = CustomField.objects.create(field_name="领导审批", order_id=60, field_type=9, field_key="leader_radio",
                                        field_choice='{"1":"同意", "2":"不同意"}', workflow=deploy_wf)
        c5 = CustomField.objects.create(field_name="运维执行", order_id=80, field_type=9, field_key="ops_radio",
                                        field_choice='{"1":"已执行", "2":"未执行"}', workflow=deploy_wf)

        # 建立初始和结束状态
        s1 = State.objects.create(name="开始", order_id=1, state_type=1, is_hidden=True, participant_type='none',
                                  workflow=deploy_wf)
        s2 = State.objects.create(name="关闭", order_id=99, state_type=2, is_hidden=True, participant_type='none',
                                  workflow=deploy_wf)
        # 建立流转状态
        s3 = State.objects.create(name="申请人-编辑中", order_id=2, participant_type='none', workflow=deploy_wf)
        s3.fields.add(c1, c2, c3)
        s4 = State.objects.create(name="领导-审批中", order_id=3, participant_type='role', workflow=deploy_wf)
        s4.fields.add(c4)
        s4.role_participant.add(role_ops_tl, role_dev_tl, role_hr_tl)
        s5 = State.objects.create(name="运维-执行中", order_id=4, participant_type='group', workflow=deploy_wf)
        s5.fields.add(c5)
        s5.group_participant.add(group_hr)
        s6 = State.objects.create(name="结束", order_id=98, state_type=2, participant_type='none', workflow=deploy_wf)

        # 建立工作流步骤
        Transition.objects.create(name=0, source_state=s1, dest_state=s3, attribute_type=0, workflow=deploy_wf)
        Transition.objects.create(name=1, source_state=s1, dest_state=s4, attribute_type=1, workflow=deploy_wf)

        Transition.objects.create(name=0, source_state=s3, dest_state=s3, attribute_type=0, workflow=deploy_wf)
        Transition.objects.create(name=1, source_state=s3, dest_state=s4, attribute_type=1, workflow=deploy_wf)
        Transition.objects.create(name=3, source_state=s3, dest_state=s6, attribute_type=3, workflow=deploy_wf)

        Transition.objects.create(name=2, source_state=s4, dest_state=s3, attribute_type=2, workflow=deploy_wf)
        Transition.objects.create(name=1, source_state=s4, dest_state=s5, attribute_type=1, workflow=deploy_wf)

        Transition.objects.create(name=2, source_state=s5, dest_state=s3, attribute_type=2, workflow=deploy_wf)
        Transition.objects.create(name=4, source_state=s5, dest_state=s2, attribute_type=5, workflow=deploy_wf)

        self.stdout.write(self.style.SUCCESS('############ 初始化角色权限 ###########'))
        menus = [34, 35, 36, 37, 38, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
                 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96]
        perms = [52, 60, 92, 96, 48, 44, 52, 73, 74, 75, 76, 85, 86, 87, 88, 81, 82, 83, 84, 77, 78, 79, 80, 28, 32, 68, 64]
        menu_obj_list = Menu.objects.filter(id__in=menus)
        perm_obj_list = Permission.objects.filter(id__in=perms)

        role_ops_tl.menus.add(*menu_obj_list)
        role_ops_tl.model_perms.add(*perm_obj_list)
        role_ops.menus.add(*menu_obj_list)
        role_ops.model_perms.add(*perm_obj_list)
        role_dev_tl.menus.add(*menu_obj_list)
        role_dev_tl.model_perms.add(*perm_obj_list)
        role_dev.menus.add(*menu_obj_list)
        role_dev.model_perms.add(*perm_obj_list)
        role_hr_tl.menus.add(*menu_obj_list)
        role_hr_tl.model_perms.add(*perm_obj_list)
        role_hr.menus.add(*menu_obj_list)
        role_hr.model_perms.add(*perm_obj_list)
        self.stdout.write(self.style.SUCCESS('发布工作流完成'))
