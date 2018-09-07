# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


# 健康问答
class CorpusHealthItem(Item):
    question = Field()                      # 问题
    answer = Field()                        # 回答，多个回答用～分开
    url = Field()                           # 问题链接


# 药品库
class MedicineItem(Item):
    Url = Field()                           # 页面url
    ImgUrl = Field()                        # 药品图片url
    DrugNames = Field()                     # 药品名称(对象包含：品牌名称、商品名称、通用名称、化学名称、英文名称)
    BrandName = Field()                     # 品牌名称
    TradeName = Field()                     # 商品名称
    GenericName = Field()                   # 通用名称
    ChemicalName = Field()                  # 化学名称
    EnglishName = Field()                   # 英文名称
    Composition = Field()                   # 成分
    Indications = Field()                   # 适应症
    DosageAndAdministration = Field()       # 用法与用量
    AdverseReactions = Field()              # 不良反应
    Contraindications = Field()             # 禁忌症
    Precautions = Field()                   # 注意事项
    SpecialDrugUse = Field()                # 特殊人群用药
    Interactions = Field()                  # 药物相互作用
    PharmacologicalActions = Field()        # 药理作用
    Storage = Field()                       # 贮藏
    Validity = Field()                      # 有效期
    ApprovalNumber = Field()                # 批准文号
    ApprovalDate = Field()                  # 批准日期
    ExpiryTime = Field()                    # 批准文号过期时间----暂时没有记录此信息
    RevisionDate = Field()                  # 说明书修订日期
    ManufacturingEnterprise = Field()       # 生产企业(对象包含：企业名称、企业简称、生产地址、联系电话)
    EnterpriseName = Field()                # 企业名称
    EnterpriseAbbreviation = Field()        # 企业简称
    ProductionAddress = Field()             # 生产地址
    ContactNumber = Field()                 # 联系电话
    Specifications = Field()                # 规格
    DosageForm = Field()                    # 剂型
    DrugProperties = Field()                # 药品属性（中西药，保健药）------根据属性搜索更新（中成药，西药）
    MedicalInsurance = Field()              # 医保类型-----39健康（只有医保和未显示）
    PrescribedDrug = Field()                # 处方药-----39健康（只有非处方药和未显示）
    Price = Field()                         # 价格------暂时没有记录此信息
    DrugCategory = Field()                  # 类别（按照治疗的疾病分类）


# 资讯
class NewsItem(Item):
    url = Field()                           # 页面url
    title = Field()                         # 标题
    content = Field()                       # 内容
    category = Field()                      # 分类


