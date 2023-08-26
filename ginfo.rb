#カード全般クラス
class Cards
	#基本プロパティ
	attr_accessor :No
	attr_accessor :type
	attr_accessor :image
	attr_accessor :name
	attr_accessor :color
	attr_accessor :summon_E
	attr_accessor :summon_AP

	#カード効果
	attr_accessor :trigger_EF
	attr_accessor :hand_never_EF

	def initialize(No:,type:,image:,name:,color:,summon_E:,summon_AP:,trigger_EF:nil,hand_never_EF:nil)
		 @No = No
		 @type = type
		 @image = image
		 @name = name
		 @color = color
		 @summon_E = summon_E
		 @summon_AP = summon_AP
		 @trigger_EF = trigger_EF
		 @hand_never_EF = hand_never_EF
	end
end

#キャラクターカードクラス
class Character < Cards
	#基礎ステータス
	attr_accessor :attribute
	attr_accessor :out_E
	attr_accessor :BP
	attr_accessor :damage

	#キーワード効果
	attr_accessor :impact
	attr_accessor :unimpact
	attr_accessor :step

	#カード効果
	attr_accessor :append_EF
	attr_accessor :main_EF
	attr_accessor :attack_EF
	attr_accessor :block_EF
	attr_accessor :void_EF
	attr_accessor :line_never_EF

	def initialize(No:,type:,image:,name:,color:,summon_E:,summon_AP:,trriger_EF:nil,hand_never_EF:nil,attribute:nil,out_E:,BP:,damage:,impact:0,unimpact:false,step:false,append_EF:nil,main_EF:nil,attack_EF:nil,block_EF:nil,void_EF:nil,line_never_EF:nil)
		super(No:No,type:type,image:image,name:name,color:color,summon_E:summon_E,summon_AP:summon_AP,trriger_EF:trigger_EF,hand_never_EF:hand_never_EF)
		@attribute = attribute
		@out_E = out_E
		@BP = BP
		@damage = damage
		@impact = impact
		@unimpact = unimpact
		@step = step
		@append_EF = append_EF
		@main_EF = main_EF
		@attack_EF = attack_EF
		@block_EF = block_EF
		@void_EF = void_EF
		@line_never_EF = line_never_EF
	end

end
