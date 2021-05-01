from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))
    password = forms.CharField(label="Password", max_length = 200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))

class PurposeForm(forms.Form):
    
    title_motivation = forms.CharField(required=False, label="Motivation",  widget=forms.TextInput(attrs= { 'style': 'visibility:hidden; height:0px; padding:0px;' } ))


    desc_motivation = forms.CharField(required=False, label=" The questions in this category are primarily intended to encourage dataset creators to clearly articulate their reasons for creating the dataset and to promote transparency about funding interests. ", widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;' } ))


    motivation_1 = forms.CharField(required=False,label="For what purpose was the dataset created?", help_text='Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    motivation_2 = forms.CharField(required=False,label="Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    motivation_3 = forms.CharField(required=False,label="Who funded the creation of the dataset?", help_text='If there is an associated grant, please provide the name of the grantor and the grant name and number.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    motivation_4 = forms.CharField(required=False,label="Any other comments?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    title_composition = forms.CharField(required=False, label="Composition",  widget=forms.TextInput(attrs= { 'style': 'visibility:hidden; height:0px; padding:0px;' } ))


    desc_composition = forms.CharField(required=False, label=" Most of these questions are intended to provide dataset consumers with the information they need to make informed decisions about using the dataset for specific tasks. The answers to some of these questions reveal information about compliance with the EU’s General Data Protection Regulation (GDPR) or comparable regulations in other jurisdictions. ", widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;' } ))


    composition_1 = forms.CharField(required=False,label="What do the instances that comprise the dataset represent (e.g., samples, images, people)?", help_text='Are there multiple types of instances (e.g., samples, images, and people), interactions (e.g., nodes and edges), resolutions (e.g., genetic data, single cell expression vs. tissue expression, cell counts, different image technologies, etc.)? Please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_2 = forms.CharField(required=False,label="How many instances are there in total?", help_text='Provide an exact integer value for each type mentioned in question C1.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_3 = forms.CharField(required=False,label="Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set?", help_text='f the dataset is a sample, then what is the larger set? Is the sample representative of the larger set (e.g., geographic coverage)? If so, please describe how this representativeness was validated/verified. If it is not representative of the larger set, please describe why not (e.g., an active decision to cover a more diverse range of instances, because instances were withheld or unavailable).', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_4 = forms.CharField(required=False,label="What data does each instance consist of?", help_text='“Raw” data (e.g., unprocessed text or images) or features? In either case, please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_5 = forms.CharField(required=False,label="Is there a label, target, or outcome (e.g., mortality) associated with each instance?", help_text='If so, please provide a description and indicate its actual presence within the dataset or whether it is represented by a proxy or compounded (e.g., a multi-cause event).', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_6 = forms.CharField(required=False,label="Is any information missing from individual instances?", help_text='If so, please provide a description, explaining why this information is missing (e.g., because it was unavailable). This does not include intentionally removed information, but might include, e.g., redacted text.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_7 = forms.CharField(required=False,label="Are relationships between individual instances made explicit (e.g., familial links, or samples derived from the same patient or same exposure)?", help_text='If so, please describe how these relationships are made explicit.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_8 = forms.CharField(required=False,label="Are there recommended data splits (e.g., training, development/validation, testing)?", help_text='If so, please provide a description of these splits, explaining the rationale behind them.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_9 = forms.CharField(required=False,label="Are there any errors, sources of noise, or redundancies in the dataset?", help_text='If so, please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_10 = forms.CharField(required=False,label="Is the dataset self-contained, or does it link to or otherwise rely on external resources (e.g., websites, public databases, other datasets and/or private silos)?", help_text='If it links to or relies on external resources, a) are there guarantees that they will exist, and remain constant, over time; b) are there official archival versions of the complete dataset (i.e., including the external resources as they existed at the time the dataset was created); c) are there any restrictions (e.g., licenses, fees) associated with any of the external resources that might apply to a future user? Please provide descriptions of all external resources and any restrictions associated with them, as well as links or other access points, as appropriate.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_11 = forms.CharField(required=False,label="Does the dataset contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor-patient confidentiality, data that includes the content of individuals’ non-public communications)?", help_text='If so, please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_12 = forms.CharField(required=False,label="Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?", help_text='If so, please describe why.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_13 = forms.CharField(required=False,label="Does the dataset not relate to people (e.g., animals, cell lines, environment)?", help_text='A short answer is sufficient. If no relation to people, you may skip the remaining questions in this section.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_14 = forms.CharField(required=False,label="Does the dataset identify any subpopulations (e.g., by age, gender, etc.)?", help_text='If so, please describe how these subpopulations are identified and provide a description of their respective distributions within the dataset.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_15 = forms.CharField(required=False,label="Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset?", help_text='If so, please describe how.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_16 = forms.CharField(required=False,label="Does the dataset contain data that might be considered sensitive in any way (e.g., data that reveals racial or ethnic origins, sexual orientations, religious beliefs, political opinions or union memberships, or locations; financial or health data; biometric or genetic data; forms of government identification, such as social security numbers; criminal history)?", help_text='If so, please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    composition_17 = forms.CharField(required=False,label="Any other comments?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    title_collectionprocess = forms.CharField(required=False, label="Collection Process",  widget=forms.TextInput(attrs= { 'style': 'visibility:hidden; height:0px; padding:0px;' } ))


    desc_collectionprocess = forms.CharField(required=False, label=" If possible, dataset creators should read through these questions prior to any data collection to flag potential issues and then provide answers once collection is complete. In addition to the goals of the prior category, the answers to questions here may provide information that allow others to reconstruct the dataset without access to it. ", widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;' } ))


    collectionprocess_1 = forms.CharField(required=False,label="How was the data associated with each instance acquired?", help_text='Was the data directly observable (e.g., raw text, instrument measurements), reported by subjects/physicians (e.g., survey responses), or indirectly inferred/derived from other data (e.g., part-of-speech tags, model-based guesses, scores, etc.)? If data was reported by subjects or indirectly inferred/derived from other data, was the data validated/verified? If so, please describe how.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_2 = forms.CharField(required=False,label="What mechanisms or procedures were used to collect the data (e.g., hardware apparatus or sensor, manual human curation, software program, software API)?", help_text='How were these mechanisms or procedures validated?', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_3 = forms.CharField(required=False,label="If the dataset is a sample from a larger set, what was the sampling strategy (e.g., deterministic, probabilistic with specific sampling probabilities)?", help_text='Please describe.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_4 = forms.CharField(required=False,label=" Who was involved in the data collection process (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., salaried, immaterial through prizes / authorship / etc) and how much (e.g., according to competitive scales mandated by [insert body or institution])?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_5 = forms.CharField(required=False,label="Over what timeframe was the data collected?", help_text='Does this timeframe match the creation timeframe of the data associated with the instances (e.g., recent data from old biobanked samples, or recent data dump from a 5-year-old registry)? If not, please describe the time frame in which the data associated with the instances was created.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_6 = forms.CharField(required=False,label="Were any ethical review processes conducted (e.g., by an institutional review board)?", help_text='If so, please provide a description of these review processes, including the outcomes, as well as a link or other access point to any supporting documentation.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_7 = forms.CharField(required=False,label="Does the dataset not relate to people (e.g., animals, cell lines, environment)?", help_text='A short answer is sufficient. If no relation to people, you may skip the remaining questions in this section.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_8 = forms.CharField(required=False,label="Did you collect the data from the individuals in question directly, or obtain it via third parties or other sources (e.g., websites)?", help_text='Please explain.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_9 = forms.CharField(required=False,label="Were the individuals in question notified about the data collection?", help_text='If so, please describe (or show with screenshots or other information) how notice was provided, and provide a link or other access point to, or otherwise reproduce, the exact language of the notification itself.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_10 = forms.CharField(required=False,label="Did the individuals in question consent to the collection and use of their data?", help_text='If so, please describe (or show with screenshots or other information) how consent was requested and provided, and provide a link or other access point to, or otherwise reproduce, the exact language to which the individuals consented.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_11 = forms.CharField(required=False,label=" If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future or for certain uses?", help_text='If so, please provide a description, as well as a link or other access point to the mechanism (if appropriate).', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_12 = forms.CharField(required=False,label="Has an analysis of the potential impact of the dataset and its use on data subjects (e.g., a data protection impact analysis) been conducted?", help_text='If so, please provide a description of this analysis, including the outcomes, as well as a link or other access point to any supporting documentation.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    collectionprocess_13 = forms.CharField(required=False,label="Any other comments?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    title_pcl = forms.CharField(required=False, label="Preprocessing, Cleaning, Labling",  widget=forms.TextInput(attrs= { 'style': 'visibility:hidden; height:0px; padding:0px;' } ))


    desc_pcl = forms.CharField(required=False, label=" If possible, dataset creators should read through these questions prior to any preprocessing, cleaning, or labeling and then provide answers once these tasks are complete. The questions in this category are intended to provide dataset consumers with the information they need to determine whether the “raw” data has been processed in ways that are compatible with their chosen tasks. ", widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;' } ))


    pcl_1 = forms.CharField(required=False,label="Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)?", help_text='If so, please provide a description. If not, you may skip the remainder of the questions in this section.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    pcl_2 = forms.CharField(required=False,label="Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)?", help_text='If so, is it available and needs to be done to gain access? If open without restriction then please describe a means to access this “raw” data.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    pcl_3 = forms.CharField(required=False,label="Is the software used to preprocess/clean/label the instances available?", help_text='If so, please provide a link or other access point and describe with enough detail so that others might reproduce it. If a custom script was used will you include it within the MAIDS repository or otherwise make it available?', widget=forms.Textarea(attrs={'class': 'form-control'}))


    pcl_4 = forms.CharField(required=False,label="Any other comments?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    title_uses = forms.CharField(required=False, label="Uses",  widget=forms.TextInput(attrs= { 'style': 'visibility:hidden; height:0px; padding:0px;' } ))


    desc_uses = forms.CharField(required=False, label=" These questions are intended to encourage dataset creators to reflect on the tasks for which the dataset should and should not be used. By explicitly highlighting these tasks, dataset creators can help dataset consumers to make informed decisions, thereby avoiding potential risks or harm. ", widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;' } ))


    uses_1 = forms.CharField(required=False,label="Has the dataset been used for any tasks already?", help_text='hers determine the value of this dataset by example.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    uses_2 = forms.CharField(required=False,label="Is there a repository that links to any or all papers or systems that use the dataset?", help_text='If so, please provide a link or other access point. Will you compile such a list and make it available in the MAIDS repository?', widget=forms.Textarea(attrs={'class': 'form-control'}))


    uses_3 = forms.CharField(required=False,label="What (other) tasks could the dataset be used for?", help_text='Please provide as much inspiration as you can. Distinguish between tasks the dataset is ideal for versus those tasks where the dataset is not entirely suited. Describe why the dataset might not be suitable ', widget=forms.Textarea(attrs={'class': 'form-control'}))


    uses_4 = forms.CharField(required=False,label="Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?", help_text='For example, is there anything that a future user might need to know to avoid uses that could result in unfair treatment of individuals or groups (e.g., stereotyping, quality of service issues) or other undesirable harms (e.g., financial harms, legal risks) If so, please provide a description. Is there anything a future user could do to mitigate these undesirable harms?', widget=forms.Textarea(attrs={'class': 'form-control'}))


    uses_5 = forms.CharField(required=False,label="Are there tasks for which the dataset should not be used?", help_text='If so, please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    uses_6 = forms.CharField(required=False,label="Any other comments?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    title_distribution = forms.CharField(required=False, label="Distribution",  widget=forms.TextInput(attrs= { 'style': 'visibility:hidden; height:0px; padding:0px;' } ))


    desc_distribution = forms.CharField(required=False, label=" Dataset creators should provide answers to these questions prior to distributing the dataset either internally within the entity on behalf of which the dataset was created or externally to third parties. ", widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;' } ))


    distribution_1 = forms.CharField(required=False,label="Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created", help_text='If so, please provide a description. If not, then disregard the rest of the questions.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    distribution_2 = forms.CharField(required=False,label="How will the dataset be distributed (e.g., tarball on website, API, GitHub)?", help_text='Does the dataset have a digital object identifier (DOI)?', widget=forms.Textarea(attrs={'class': 'form-control'}))


    distribution_3 = forms.CharField(required=False,label="When will the dataset be distributed?", help_text='A cautious response is more useful than an optimistic one.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    distribution_4 = forms.CharField(required=False,label="Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)?", help_text='If so, please describe this license and/or ToU, and provide a link or other access point to, or otherwise reproduce, any relevant licensing terms or ToU, as well as any fees associated with these restrictions.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    distribution_5 = forms.CharField(required=False,label="Have any third-parties imposed IP-based or other restrictions on the data associated with the instances?", help_text='If so, please describe these restrictions, and provide a link or other access point to, or otherwise reproduce, any relevant licensing terms, as well as any fees associated with these restrictions.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    distribution_6 = forms.CharField(required=False,label="Do any export controls or other regulatory restrictions apply to the dataset or to individual instances?", help_text='If so, please describe these restrictions, and provide a link or other access point to, or otherwise reproduce, any supporting documentation.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    distribution_7 = forms.CharField(required=False,label="Any other comments?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    title_maintenance = forms.CharField(required=False, label="Maintenance",  widget=forms.TextInput(attrs= { 'style': 'visibility:hidden; height:0px; padding:0px;' } ))


    desc_maintenance = forms.CharField(required=False, label=" As with the previous category, dataset creators should provide answers to these questions prior to distributing the dataset. These questions are intended to encourage dataset creators to plan for dataset maintenance and communicate this plan with dataset consumers. ", widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;' } ))


    maintenance_1 = forms.CharField(required=False,label="Who is supporting/hosting/maintaining the dataset?", help_text='Please be as thorough as possible.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    maintenance_2 = forms.CharField(required=False,label="How can the owner/curator/manager of the dataset be contacted (e.g., email address)?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    maintenance_3 = forms.CharField(required=False,label="Is there an erratum?", help_text='If so, please provide a link or other access point.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    maintenance_4 = forms.CharField(required=False,label="Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)?", help_text='If so, please describe how often, by whom, and how updates will be communicated to users (e.g., mailing list, GitHub)?', widget=forms.Textarea(attrs={'class': 'form-control'}))


    maintenance_5 = forms.CharField(required=False,label="If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances (e.g., were individuals in question told that their data would be retained for a fixed period of time and then deleted)?", help_text='If so, please describe these limits and explain how they will be enforced.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    maintenance_6 = forms.CharField(required=False,label="Will older versions of the dataset continue to be supported/hosted/maintained?", help_text='If so, please describe how. If not, please describe how its obsolescence will be communicated to users.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    maintenance_7 = forms.CharField(required=False,label="If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?", help_text='If so, please provide a description. Will these contributions be validated/verified? If so, please describe how. If not, why not? Is there a process for communicating/distributing these contributions to other users? If so, please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))


    maintenance_8 = forms.CharField(required=False,label="Any other comments?", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))

class DocumentForm(forms.Form):
    subsets = forms.FileField(label='Select a file for subsets (around 1000 x 1000 )')
    thematic = forms.FileField(label='Select a file for thematic ')

class AboutForm(forms.Form):
    
    title = forms.CharField(required=False, label=" What is the title of your dataset?", widget=forms.TextInput(attrs={'class':'form-control' } ))

    authors = forms.CharField(required=False, label=" Who are the dataset's authors? (provide fullnames)",help_text=' Use comma between names if there are multiple people, use blank space to separare first name and last names', widget=forms.TextInput(attrs={'class':'form-control' } ))


    abstract = forms.CharField(required=False, label=" Please provide a brief abstract describing this dataset.", widget=forms.TextInput(attrs={'class':'form-control' } )) 


    research_main = forms.CharField(required=False,label="Please state, in detail, the main hypothesis for which this dataset was created.", help_text='', widget=forms.Textarea(attrs={'class': 'form-control'}))


    research_secondary = forms.CharField(required=False,label="Please state, in detail, any other hypotheses which this dataset would be able to address.", help_text='If there is an associated grant, please provide the name of the grantor and the grant name and number.', widget=forms.Textarea(attrs={'class': 'form-control'}))



#dynamic form
class MyForm(forms.Form):
    #original_field = forms.CharField(required=False)
    extra_field_count = forms.CharField(widget=forms.HiddenInput())
    extra_ft_count = forms.CharField(widget=forms.HiddenInput()) # extra_feature was changed to extra_ft because we will be filtering all fields that contain the word "feature". 
    
    
    
    
    
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)
        extra_ft = kwargs.pop('extra_ft', 0) # extra_features was changed to extra_ft because we will be filtering all fields that contain the word "feature". 

        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields
        
        print("--------------------------------")
        print("--------------------------------")
        print("--------------------------------")
        print("extra_fields are gonna be iterated")
        print(extra_fields)
        print("--------------------------------")
        print("--------------------------------")
        print("--------------------------------")
        print("--------------------------------")
        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['subset_{index}_title'.format(index=index)] = \
                forms.CharField(required=False, label="Subset {index}".format(index = index),  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            
            self.fields['subset_{index}_1'.format(index=index)] = \
                forms.CharField(label = "What is the ID of the Subset?")
  
            self.fields['subset_{index}_2'.format(index=index)] = \
                forms.CharField(label = "What is the Name of the Subset?")
            self.fields['subset_{index}_3'.format(index=index)] = \
                forms.CharField(required=False, label = "When was the subset last updated?")
            self.fields['subset_{index}_4'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the modality of the subset? (The type of data)")
            self.fields['subset_{index}_5'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the format or the schema of the subset?")
            self.fields['subset_{index}_6'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the size of the subset? (Number of rows if it's a table or files if it's a directory)")
            self.fields['subset_{index}_7'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the ID of the parent of the subset? (Use 0 if none)")
            self.fields['subset_{index}_8'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the purpose of the subset?")
            self.fields['subset_{index}_9'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the link (URL) to further description of the subset?")
            self.fields['subset_{index}_10'.format(index=index)] = \
                forms.CharField(required=False, label = "Have you calculated a covariance matrix (or similar) and made it available in this dataset? Where?")
            self.fields['subset_{index}_11'.format(index=index)] = \
                forms.CharField(required=False, label = "Have you modeled all (or a few) features and made the models accessible in this dataset? Where?")

        try:
            self.fields['subset_0_5'].initial = "hello this is a test"
            print("Did it ")
        except:
            print("Did not do it")
        

        self.fields['extra_ft_count'].initial = extra_ft
         
        for index in range(int(extra_ft)):
            # generate extra fields in the number specified via extra_fields
            self.fields['feature_{index}_title'.format(index=index)] = \
                forms.CharField(required=False, label="Feature {index}".format(index = index),  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            self.fields['feature_{index}_1'.format(index=index)] = \
                forms.CharField(label = "What is the ID of the Feature?")
            self.fields['feature_{index}_2'.format(index=index)] = \
                forms.CharField(label = "What is the ID of the reference subset of the feature?")
            self.fields['feature_{index}_3'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the introduction date of the feature?")
            self.fields['feature_{index}_4'.format(index=index)] = \
                forms.CharField(label = "What is the Name of the Feature?")
            self.fields['feature_{index}_5'.format(index=index)] = \
                forms.CharField(required=False, label = "What are the values that the feature might take?")
            self.fields['feature_{index}_6'.format(index=index)] = \
                forms.CharField(required=False, label = "What special meaning does NA, NULL, NONE, or any other placeholder have with respect to this feature?")
            self.fields['feature_{index}_7'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the meaning of the feature if it is zero?")
            self.fields['feature_{index}_8'.format(index=index)] = \
                forms.CharField(required=False, label = "What does it mean if no value is to be found?")
            self.fields['feature_{index}_9'.format(index=index)] = \
                forms.CharField(required=False, label = "What level of non-zero sparsity is there?")
            self.fields['feature_{index}_10'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the mean if the feature is nummeric?")
            self.fields['feature_{index}_11'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the standard deviation if the feature is numeric?")
            self.fields['feature_{index}_12'.format(index=index)] = \
                forms.CharField(required=False, label = "How many modes does the feature have?")
            self.fields['feature_{index}_13'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the median value?")
            self.fields['feature_{index}_14'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the inter quartile range?")
            self.fields['feature_{index}_15'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the ID of the parent feature (If derived from other features)")
            self.fields['feature_{index}_16'.format(index=index)] = \
                forms.CharField(required=False, label = "What unit is this feature in?")
            self.fields['feature_{index}_17'.format(index=index)] = \
                forms.CharField(required=False, label = "Define the feature.")
            self.fields['feature_{index}_18'.format(index=index)] = \
                forms.CharField(required=False, label = "Why does the feature exist or is it superfluous?")
            self.fields['feature_{index}_19'.format(index=index)] = \
                forms.CharField(required=False, label = "State whether the feature is encoded and what the mapping is.")